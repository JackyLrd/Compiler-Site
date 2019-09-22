class foo
{
    public:
        foo(int x, int y):a(x), b(y), wtf(nullptr) {}
        void func();
    private:
        int a;
        int b;
        char * * wtf;
};