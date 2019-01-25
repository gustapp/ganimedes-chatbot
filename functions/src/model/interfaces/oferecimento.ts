import { IHorario as Horario } from './horario';

export interface IOferecimento {
    codigo_turma: String,
    tipo_turma: String,
    horario: Horario[]
}