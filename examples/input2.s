.data
print_int_fmt: .string "%ld \n"
print_str_fmt: .string "%s \n"
.text
.data
print_fmt: .string "%ld \n"
.text
.data
truck:
 .zero 8
.text
.globl main
main:
 pushq %rbp
 movq %rsp, %rbp
 subq $24, %rsp
 movq $10, %rax
 movq %rax, -8(%rbp)
 movq $20, %rax
 movq %rax, 0(%rbp)
 movq 0(%rbp), %rax
 movq %rax, -24(%rbp)
 movq -24(%rbp), %rax
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
 movq -8(%rbp), %rax
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
 movq -8(%rbp), %rax
 movq %rax, truck(%rip)
 movq truck(%rip), %rax
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
 movq -24(%rbp), %rax
 movq %rax, truck(%rip)
 movq truck(%rip), %rax
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
 movq $0, %rax
 jmp .end_main
.end_main:
leave
ret
.section note.GNU-stack,"",@progbits
