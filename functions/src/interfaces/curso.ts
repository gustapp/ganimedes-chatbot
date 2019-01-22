import { ICredito as Credito } from './credito';
import { IDocente as Docente } from './docente';
import { IAvaliacao as Avaliacao } from './avaliacao';
import { IRequisito as Requisito } from './requisito';
import { IOferecimento as Oferecimento } from './oferecimento';

export interface ICurso {
    sigla: String,
    name: String,
    creditos: Credito,
    carga_horaria: Number,
    objetivos: String,
    docentes: Docente[],
    programa: String,
    programa_resumido: String,
    avaliacao: Avaliacao,
    bibliografia: String[],
    requisitos: Requisito[],
    oferecimento: Oferecimento[]
}