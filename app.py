import sys
import sys
import os
import subprocess # <--- Necesario para ejecutar ./a.out
import time
import shutil
# --- 1. Clase de la Máquina Virtual ---

class Machine:
    def __init__(self, entry_pc, labels_map, stack_size=256):
        self.registers_map = {
            "%rax": 0, "%rbx": 0, "%rcx": 0, "%rdx": 0,
            "%rsi": 0, "%rdi": 0, "%rbp": 0, "%rsp": 0,
            "%r8": 0, "%r9": 0, "%r10": 0, "%r11": 0,
            "%r12": 0, "%r13": 0, "%r14": 0, "%r15": 0
        }

        self.reg_aliases = {
            "%eax": "%rax", "%al": "%rax",
            "%ebx": "%rbx", "%bl": "%rbx",
            "%ecx": "%rcx", "%cl": "%rcx",
            "%edx": "%rdx", "%dl": "%rdx",
            "%esi": "%rsi", "%edi": "%rdi"
        }

        self.flags = {'ZF': 0, 'SF': 0}
        self.pc = entry_pc
        self.labels_map = labels_map
        self.stack_size = stack_size
        self.stack = [0] * stack_size
        
        # Inicializar Stack Pointers al final de la memoria
        initial_sp = (stack_size - 1) * 8
        self.registers_map['%rsp'] = initial_sp
        self.registers_map['%rbp'] = initial_sp

    def _resolve_reg(self, reg_name):
        """Devuelve el nombre canónico del registro (ej: %eax -> %rax)"""
        return self.reg_aliases.get(reg_name, reg_name)

    def get_reg_value(self, reg_name):
        real_reg = self._resolve_reg(reg_name.strip())
        return self.registers_map.get(real_reg, 0)

    def set_reg_value(self, reg_name, value):
        real_reg = self._resolve_reg(reg_name.strip())
        self.registers_map[real_reg] = value

    def push(self, value):
        self.registers_map['%rsp'] -= 8
        stack_index = self.registers_map['%rsp'] // 8
        if 0 <= stack_index < self.stack_size:
            self.stack[stack_index] = value
        else:
            print("ERROR: Stack Overflow")
            sys.exit()

    def pop(self):
        rsp_addr = self.registers_map['%rsp']
        stack_index = rsp_addr // 8
        if 0 <= stack_index < self.stack_size:
            value = self.stack[stack_index]
            self.registers_map['%rsp'] += 8 # Liberar espacio
            return value
        else:
            print("ERROR: Stack Underflow")
            sys.exit()

    def display_state(self, current_line_number):
        # Devolvemos una lista limpia, sin indentación forzada.
        # El centrado lo hará la función run_simulator.
        
        lines = []
        lines.append("") # Espacio
        lines.append("--- ESTADO DE LA MÁQUINA ---")
        lines.append(f"PC (Línea): {current_line_number}")
        lines.append("Flags: ZF={} SF={}".format(self.flags['ZF'], self.flags['SF']))
        
        lines.append("")
        lines.append("--- REGISTROS (Hex) ---")

        # Formatear registros en 2 columnas compactas
        claves = sorted(list(self.registers_map.keys()))
        half = len(claves) // 2
        for i in range(half):
            reg1 = claves[i]
            reg2 = claves[i+half]
            val1 = f"0x{self.registers_map[reg1]:016x}"
            val2 = f"0x{self.registers_map[reg2]:016x}"
            # String formateado rígidamente
            lines.append(f"{reg1:<4}: {val1}  {reg2:<4}: {val2}")

        lines.append("")
        lines.append("--- PILA (Top 10) ---")
        
        rsp_addr = self.registers_map['%rsp']
        rsp_index = rsp_addr // 8
        
        if rsp_index < 0 or rsp_index >= self.stack_size:
            lines.append(">> RSP fuera de límites <<")
        else:
            # Encabezado de tabla simple
            lines.append(f"{'DIR':<8} | {'VALOR (Hex)':<12}")
            lines.append("-" * 25)
            for i in range(10): # Mostramos 10 elementos
                current_index = rsp_index + i
                if current_index < self.stack_size:
                    value = self.stack[current_index]
                    addr = rsp_addr + (i * 8)
                    # Formato tabla
                    lines.append(f"0x{addr:04x}   | 0x{value:<10x}")
                else:
                    lines.append(f"0x????   | 0x0")
        return lines



# --- 2. Lógica de Instrucciones ---

def parse_operand(operand, machine):
    operand = operand.strip()
    if operand.startswith('$'):
        return int(operand[1:]), 'imm'
    elif operand.startswith('%'):
        return machine.get_reg_value(operand), 'reg'
    elif '(' in operand:
        # Memoria: D(Rb)
        if ')' in operand:
            offset_str, base_reg = operand.split('(')
            base_reg = base_reg.strip(')').strip()
            offset = int(offset_str) if offset_str else 0
            
            base_addr = machine.get_reg_value(base_reg)
            mem_index = (base_addr + offset) // 8
            
            if 0 <= mem_index < machine.stack_size:
                return machine.stack[mem_index], 'mem'
            else:
                print(f"ERROR: Acceso a memoria inválido: {operand}")
                sys.exit()
    try:
        return int(operand), 'imm'
    except ValueError:
        return 0, 'unknown'

def execute_instruction(machine, instruction):
    cleaned_instruction = instruction.replace(',', ' ')
    parts = cleaned_instruction.strip().split()
    if not parts: return
    opcode = parts[0].upper()
    operands = parts[1:]
    # operands = [op.strip(',') for op in parts[1:]]

    if opcode == 'PUSHQ':
        src_val, _ = parse_operand(operands[0], machine)
        machine.push(src_val)

    elif opcode == 'POPQ':
        dest_reg = operands[0]
        val = machine.pop()
        machine.set_reg_value(dest_reg, val)


    elif opcode in ['MOVQ', 'MOVL', 'MOVZBQ']: 
        # Tratamos movl y movzbq como movq simple para este nivel de simulación
        if len(operands) < 2: return
        src_val, _ = parse_operand(operands[0], machine)
        dest_operand = operands[1]

        if dest_operand.startswith('%'):
            machine.set_reg_value(dest_operand, src_val)
        elif '(' in dest_operand:
            # Lógica de escritura en memoria
            offset_str, base_reg = dest_operand.split('(')
            base_reg = base_reg.strip(')').strip()
            offset = int(offset_str) if offset_str else 0
            base_addr = machine.get_reg_value(base_reg)
            mem_index = (base_addr + offset) // 8
            if 0 <= mem_index < machine.stack_size:
                machine.stack[mem_index] = src_val


    elif opcode == 'SUBQ':
        val, _ = parse_operand(operands[0], machine)
        dest = operands[1]
        machine.set_reg_value(dest, machine.get_reg_value(dest) - val)
        
    elif opcode == 'ADDQ':
        val, _ = parse_operand(operands[0], machine)
        dest = operands[1]
        machine.set_reg_value(dest, machine.get_reg_value(dest) + val)

    elif opcode == 'IMULQ':
        val, _ = parse_operand(operands[0], machine)
        dest = operands[1]
        machine.set_reg_value(dest, machine.get_reg_value(dest) * val)


    elif opcode == 'LEAQ': # Agregado por si acaso, útil para printf        
         # leaq label(%rip), %reg -> simplificado, solo tomamos la etiqueta como dirección ficticia
         # Para este simulador simple, ignoramos la aritmética de direcciones real de LEA
         pass


    elif opcode == 'CMPQ':
        # CMP src, dest  -> Realiza (dest - src) y actualiza flags
        src_val, _ = parse_operand(operands[0], machine)
        dest_val, _ = parse_operand(operands[1], machine)
        
        result = dest_val - src_val
        
        # Actualizar Flags
        machine.flags['ZF'] = 1 if result == 0 else 0
        machine.flags['SF'] = 1 if result < 0 else 0
        # (Nota: Ignoramos Overflow Flag OF por simplicidad, asumimos enteros normales)

    elif opcode == 'SETG':
        # Set if Greater (Signed): Pone 1 en el destino si ZF=0 y SF=OF (aquí SF=0)
        # Es decir, si el resultado de la resta anterior fue positivo estricto.
        condition = (machine.flags['ZF'] == 0 and machine.flags['SF'] == 0)
        dest_reg = operands[0]
        machine.set_reg_value(dest_reg, 1 if condition else 0)

    elif opcode == 'SETLE':
        # Set if Less or Equal (<=): (ZF=1 o SF=1)
        # Significa: Son iguales (ZF=1) O el resultado fue negativo (SF=1)
        # Nota: Asumimos que no hubo Overflow (OF) para simplificar
        condition = (machine.flags['ZF'] == 1 or machine.flags['SF'] == 1)
        dest_reg = operands[0]
        machine.set_reg_value(dest_reg, 1 if condition else 0)

    elif opcode == 'SETE':
        # Set if Equal (==): (ZF=1)
        condition = (machine.flags['ZF'] == 1)
        dest_reg = operands[0]
        machine.set_reg_value(dest_reg, 1 if condition else 0)

    elif opcode == 'SETNE':
        # Set if Not Equal (!=): (ZF=0)
        condition = (machine.flags['ZF'] == 0)
        dest_reg = operands[0]
        machine.set_reg_value(dest_reg, 1 if condition else 0)

    elif opcode == 'CALL':
        label = operands[0]
        if label == 'printf@PLT':
            val_to_print = machine.get_reg_value('%rsi') # 2do argumento
            # Pequeño hack para detectar si es string (formato %s) o int
            fmt_reg = machine.get_reg_value('%rdi') # 1er argumento (formato)
            # Como no tenemos memoria estática real (.data), asumimos entero por ahora
            print(f">>> 🖥️ OUTPUT: {val_to_print}")
        elif label in machine.labels_map:
            machine.push(machine.pc + 1)
            machine.pc = machine.labels_map[label] - 1
        else:
            print(f"ERROR: Call a etiqueta desconocida '{label}'")  


    elif opcode == 'RET':
        ret_addr = machine.pop()
        machine.pc = ret_addr - 1

    elif opcode == 'LEAVE':
        # movq %rbp, %rsp
        machine.set_reg_value('%rsp', machine.get_reg_value('%rbp'))
        # popq %rbp
        old_rbp = machine.pop()
        machine.set_reg_value('%rbp', old_rbp)
    
    elif opcode == 'JMP':
        label = operands[0]
        if label in machine.labels_map:
            machine.pc = machine.labels_map[label] - 1
            
    elif opcode == 'JE': # Jump if Equal
        label = operands[0]
        if machine.flags['ZF'] == 1:
            if label in machine.labels_map:
                machine.pc = machine.labels_map[label] - 1

    # IMPORTANTE: Avanzar el PC siempre
    machine.pc += 1

# --- 3. El Motor Principal (Corregido) ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_simulator(assembly_code):
    # --- PREPARACIÓN (Igual que antes) ---
    lines = assembly_code.split('\n')
    indexed_instructions = []
    labels_map = {}
    
    line_number = 1
    for line in lines:
        stripped = line.strip().replace('\t', '    ')
        if not stripped: continue
        if stripped.endswith(':'):
            label_name = stripped[:-1]
            labels_map[label_name] = line_number + 1
            indexed_instructions.append((line_number, stripped))
            line_number += 1
            continue
        if stripped.startswith('.'):
             indexed_instructions.append((line_number, stripped))
             line_number += 1
             continue
        indexed_instructions.append((line_number, stripped))
        line_number += 1

    entry_pc = labels_map.get('main', 0)
    if entry_pc == 0: entry_pc = 1

    machine = Machine(entry_pc, labels_map)
    auto_run = False 

    # --- BUCLE PRINCIPAL ---
    while True:
        # 1. Obtener dimensiones actuales de la consola
        # columns: ancho total en caracteres
        terminal_size = shutil.get_terminal_size()
        cols = terminal_size.columns
        
        # 2. Calcular mitades exactas
        # Restamos un poco para el borde y el separador central
        # Estructura: [ IZQUIERDA ] ║ [ DERECHA ]
        mid_point = cols // 2
        
        # Ancho útil para cada columna (restamos espacio para el separador " ║ ")
        col_width = mid_point - 2 

        current_pc = machine.pc
        
        if not auto_run:
            clear_screen()
        else:
            time.sleep(0.05) 
            clear_screen()

        # 3. Buscar instrucción
        current_instr_tuple = next((t for t in indexed_instructions if t[0] == current_pc), None)
        
        if not current_instr_tuple:
            if current_pc <= len(indexed_instructions) + 5:
                 machine.pc += 1
                 continue
            print("\n🛑 FIN DEL PROGRAMA.")
            break
            
        current_src = current_instr_tuple[1]
        
        # 4. Preparar contenido de paneles
        state_panel = machine.display_state(current_pc)
        code_panel = []
        for ln, instr in indexed_instructions:
            marker = "" if ln == current_pc else "  "
            # Formateamos la línea de código
            line_content = f"{marker} {ln:02}: {instr}"
            code_panel.append(line_content)

        # 5. RENDERIZADO DINÁMICO (Responsive)
        
        # Encabezado que se adapta al ancho
        print("\n" + "═" * cols)
        header_text = f" X86 PLAYGROUND | PC: {current_pc} | INSTR: {current_src}"
        # Centrar el texto del header y cortar si es muy largo
        print(f"{header_text[:cols-1].center(cols)}") 
        print("─" * cols)
        
        max_lines = max(len(code_panel), len(state_panel))
        
        for i in range(max_lines):
            # Obtener texto crudo de cada lado
            raw_left = code_panel[i] if i < len(code_panel) else ""
            raw_right = state_panel[i] if i < len(state_panel) else ""
            
            # MAGIA: Cortar y Rellenar (Slicing & Padding)
            # 1. [:col_width] -> Corta el texto si es más largo que la mitad (evita que empuje la barra)
            # 2. .ljust(col_width) -> Rellena con espacios si es más corto (mantiene la barra fija)
            
            final_left = raw_left[:col_width].ljust(col_width)
            final_right = raw_right[:col_width].ljust(col_width)
            
            # Imprimir la línea con el separador fijo en el medio
            print(f"{final_left} ║ {final_right}")
            
        print("═" * cols)

        # 6. Ejecutar lógica
        if current_src.endswith(':') or current_src.startswith('.'):
            machine.pc += 1
        else:
            execute_instruction(machine, current_src)

        # 7. Inputs
        if auto_run: continue

        try:
            print(f"[ENTER] Step | [r] Restart | [q] Quit")
            # Usamos input sin texto para no romper la estética, o uno minimalista
            command = input("> ").strip().lower()

            if command == 'q': sys.exit(0)
            elif command == 'r':
                machine = Machine(entry_pc, labels_map)
                continue
            else: pass

        except KeyboardInterrupt:
            sys.exit(0)



# --- 5. Punto de Entrada (Main: Compilador + Simulador) ---

def main():
    # 1. Verificación de argumentos
    if len(sys.argv) < 3:
        print("\n❌ Error: Debes indicar el archivo de código fuente (pseudo-C).")
        print("Uso correcto: python3 test.py <archivo.txt>")
        sys.exit(1)

    source_file = sys.argv[2]
    
    # Verificamos que el archivo input exista
    if not os.path.exists(source_file):
        print(f"❌ Error: El archivo '{source_file}' no existe.")
        sys.exit(1)

    # 2. Paso de Compilación (Ejecutar ./a.out)
    print(f"🔨 Compilando '{source_file}' con ./compiler ...")
    
    executable = sys.argv[1]
    
    # Verificamos si a.out existe y es ejecutable
    if not os.path.exists(executable):
         print(f"❌ Error: No se encuentra el compilador '{executable}'.")
         sys.exit(1)

    try:
        # subprocess.run ejecuta el comando en la terminal
        # check=True lanza una excepción si a.out devuelve error
        subprocess.run([executable, source_file], check=True)
        print("✅ Compilación exitosa.")
        
    except subprocess.CalledProcessError:
        print("\n❌ Error: La compilación falló (tu compiler reportó un error).")
        sys.exit(1)
    except PermissionError:
        print(f"\n❌ Error: No tienes permisos para ejecutar '{executable}'. Intenta: chmod +x compiler")
        sys.exit(1)

    # 3. Determinar el nombre del archivo .s generado
    # Asumimos la lógica: input.txt -> input.s
    base_name = os.path.splitext(source_file)[0] # Quita la extensión .txt
    assembly_file = base_name + ".s"

    # 4. Cargar el Assembly y Simular
    if not os.path.exists(assembly_file):
        print(f"❌ Error: Se esperaba que se creara '{assembly_file}', pero no aparece.")
        sys.exit(1)

    print(f"📂 Leyendo assembly generado: {assembly_file} ...")
    
    try:
        with open(assembly_file, 'r') as file:
            assembly_code = file.read()
            
        if not assembly_code.strip():
            print(f"⚠️ El archivo '{assembly_file}' está vacío.")
            sys.exit(1)

        # --- EJECUTAR SIMULADOR ---
        run_simulator(assembly_code)

    except Exception as e:
        print(f"\n❌ Error leyendo el archivo assembly: {e}")

if __name__ == "__main__":
    main()
