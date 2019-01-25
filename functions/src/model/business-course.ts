interface Assessment {
    metodo: String,
    criterio: String,
    recuperacao: String
}

interface Credits {
    aula: number,
    trabalho: number
}

interface Requirement {
    nome: String
}

interface Class {
    codigo_turma: String,
    tipo_turma: String,
    horario: Schedule[]
}

interface Schedule {
    dia: String,
    horario_inicio: String,
    horario_fim: String,
    professor: String
}

interface ICourse {
    initials: string;
    name: string;
    credits: Credits;
    workload: number;
    objectives: string;
    teachers: string[];
    syllabus: string;
    abstract: string;
    assessment: Assessment;
    bibliograph: string[];
    requirements: Requirement[];
    getClasses() : Class[];
}

export class CourseProxy implements ICourse {
    private course: ICourse;

    constructor(readonly initials: string, readonly name: string, readonly objectives: string, readonly teachers: string[], readonly abstract: string, 
        readonly syllabus: string, readonly assessment: Assessment, readonly bibliograph: string[], readonly workload: number, readonly credits: Credits, readonly requirements: Requirement[]){}

    public getClasses() : Class[] {
        // if (!this.course) {
        //     course = .getPessoaByID(this.id);
        // }
        return this.course.getClasses();
    }
}

export class Course implements ICourse{

    constructor(private classes: Class[], readonly initials: string, readonly name: string, readonly objectives: string, readonly teachers: string[], readonly abstract: string, 
        readonly syllabus: string, readonly assessment: Assessment, readonly bibliograph: string[], readonly workload: number, readonly credits: Credits, readonly requirements: Requirement[]){}

    public getClasses() : Class[] {
        return this.classes;
    }
}