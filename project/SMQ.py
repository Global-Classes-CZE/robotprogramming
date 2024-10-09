class SMQ:
    __NO = 0
    __Q = {}

    @staticmethod
    def add(sm: 'StateAbstract', smq_no_parent: int | None = None) -> 'StateAbstract':
        SMQ.__NO += 1
        sm.smq_no(SMQ.__NO)
        SMQ.__Q[SMQ.__NO] = [sm, smq_no_parent]
        return sm

    @staticmethod
    def parentOf(smq_no: int) -> 'StateAbstract' | None:
        smq_no_parent = SMQ.__Q[smq_no][1]
        if smq_no_parent is None:
            return None
        return SMQ.__Q[smq_no_parent][0]

    @staticmethod
    def remove(smq_no: int):
        del SMQ.__Q[smq_no]

    @staticmethod
    def tick():
        for k, n in SMQ.__Q.items():
            n[0].tick()
