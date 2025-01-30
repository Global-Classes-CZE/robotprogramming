class CPU:
    __NO = 0
    __Q = {}

    @staticmethod
    def add(sm: 'AbstractSM', cpu_no_parent: int | None = None) -> 'AbstractSM':
        CPU.__NO += 1
        sm.cpu_no(CPU.__NO)
        CPU.__Q[CPU.__NO] = [sm, cpu_no_parent]
        sm.run()
        return sm

    @staticmethod
    def parentOf(cpu_no: int) -> 'AbstractSM' | None:
        cpu_no_parent = CPU.__Q[cpu_no][1]
        if cpu_no_parent is None:
            return None
        return CPU.__Q[cpu_no_parent][0]

    @staticmethod
    def remove(cpu_no: int):
        del CPU.__Q[cpu_no]

    @staticmethod
    def tick():
        for k, n in CPU.__Q.items():
            n[0].tick()
