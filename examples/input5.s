.data
print_int_fmt: .string "%ld \n"
print_str_fmt: .string "%s \n"
.text
.data
print_fmt: .string "%ld \n"
.text
.data
matriz:
 .zero 24
.text
.globl main
main:
 pushq %rbp
 movq %rsp, %rbp
 subq $8, %rsp
 movq $40, %rax
 pushq %rax
 movq $0, %rax
 movq %rax, %rcx
 imulq $8, %rcx
 leaq matriz(%rip), %rax
 addq %rcx, %rax
 popq %rcx
 movq %rcx, (%rax)
 movq $50, %rax
 pushq %rax
 movq $1, %rax
 movq %rax, %rcx
 imulq $8, %rcx
 leaq matriz(%rip), %rax
 addq %rcx, %rax
 popq %rcx
 movq %rcx, (%rax)
 movq $60, %rax
 pushq %rax
 movq $2, %rax
 movq %rax, %rcx
 imulq $8, %rcx
 leaq matriz(%rip), %rax
 addq %rcx, %rax
 popq %rcx
 movq %rcx, (%rax)
 movq $5, %rax
 pushq %rax
 movq $1, %rax
 movq %rax, %rcx
 imulq $8, %rcx
 leaq matriz(%rip), %rax
 addq %rcx, %rax
 movq (%rax), %rax
 movq %rax, %rcx
 popq %rax
 xchgq %rax, %rcx
 addq %rcx, %rax
 movq %rax, -8(%rbp)
 movq -8(%rbp), %rax
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
