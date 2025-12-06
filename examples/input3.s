.data
print_int_fmt: .string "%ld \n"
print_str_fmt: .string "%s \n"
.text
.data
print_fmt: .string "%ld \n"
.text
.data
g1:
 .quad 1
 .quad 2
 .quad 3
.text
.globl average
average:
 pushq %rbp
 movq %rsp, %rbp
 subq $32, %rsp
 movq %rdi,-8(%rbp)
 movq %rsi,-16(%rbp)
 movq $0, %rax
 movq %rax, -24(%rbp)
 movq $0, %rax
 movq %rax, -32(%rbp)
while_0:
 movq -32(%rbp), %rax
 pushq %rax
 movq -16(%rbp), %rax
 movq %rax, %rcx
 popq %rax
 cmpq %rcx, %rax
 movl $0, %eax
 setle %al
 movzbq %al, %rax
 cmpq $0, %rax
 je endwhile_0
 movq -24(%rbp), %rax
 movq %rax, %rcx
 movq -32(%rbp), %rax
 movq %rax, %rcx
 imulq $8, %rcx
 movq -8(%rbp), %rax
 addq %rcx, %rax
 movq (%rax), %rax
 addq %rcx, %rax
 movq %rax, -24(%rbp)
 movq -32(%rbp), %rax
 pushq %rax
 movq $1, %rax
 movq %rax, %rcx
 popq %rax
 addq %rcx, %rax
 movq %rax, -32(%rbp)
 jmp while_0
endwhile_0:
 movq -24(%rbp), %rax
 jmp .end_average
.end_average:
leave
ret
.globl main
main:
 pushq %rbp
 movq %rsp, %rbp
 subq $24, %rsp
 movq $4, %rax
 movq %rax, -24(%rbp)
 movq $5, %rax
 movq %rax, -16(%rbp)
 movq $6, %rax
 movq %rax, -8(%rbp)
 movq $0, %rax
 movq %rax, %rcx
 imulq $8, %rcx
 leaq g1(%rip), %rax
 addq %rcx, %rax
 movq (%rax), %rax
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
 movq $1, %rax
 movq %rax, %rcx
 imulq $8, %rcx
 leaq g1(%rip), %rax
 addq %rcx, %rax
 movq (%rax), %rax
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
 movq $2, %rax
 movq %rax, %rcx
 imulq $8, %rcx
 leaq g1(%rip), %rax
 addq %rcx, %rax
 movq (%rax), %rax
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
 movq $0, %rax
 movq %rax, %rcx
 imulq $8, %rcx
 leaq -24(%rbp), %rax
 addq %rcx, %rax
 movq (%rax), %rax
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
 movq $1, %rax
 movq %rax, %rcx
 imulq $8, %rcx
 leaq -24(%rbp), %rax
 addq %rcx, %rax
 movq (%rax), %rax
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
 movq $2, %rax
 movq %rax, %rcx
 imulq $8, %rcx
 leaq -24(%rbp), %rax
 addq %rcx, %rax
 movq (%rax), %rax
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
 leaq g1(%rip), %rdi
 movq $3, %rax
 movq %rax, %rsi
call average
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
 leaq -24(%rbp), %rdi
 movq $3, %rax
 movq %rax, %rsi
call average
 movq %rax, %rsi
 leaq print_int_fmt(%rip), %rdi
 movl $0, %eax
 call printf@PLT
.end_main:
leave
ret
.section note.GNU-stack,"",@progbits
