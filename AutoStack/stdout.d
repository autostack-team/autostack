syscall::write*:entry
/arg0 == 2/ {
    printf("%s", copyinstr(arg1, arg2));
}