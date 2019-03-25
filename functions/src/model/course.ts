import { ClassRepository } from "../data-access/class-repository";
import { Reference } from './reference';
import { ClassProxy } from "./class";

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
    getClasses() : any;
}

export class CourseProxy extends Reference implements ICourse {
    private course: ICourse;

    constructor(docRef: FirebaseFirestore.DocumentReference, readonly initials: string, readonly name: string, readonly objectives: string, readonly teachers: string[], readonly abstract: string, 
            readonly syllabus: string, readonly assessment: Assessment, readonly bibliograph: string[], readonly workload: number, readonly credits: Credits, readonly requirements: Requirement[]){
        super(docRef);
    }

    public async getClasses(): Promise<ClassProxy[]>{
        if (!this.course) {
            const daClass = this.daHelper
                .create(ClassRepository);

            const classes = await daClass.getColl();

            return classes;
        }
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