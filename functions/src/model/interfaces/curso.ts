import { ICredito as Credito } from './credito';
import { IDocente as Docente } from './docente';
import { IAvaliacao as Avaliacao } from './avaliacao';
import { IRequisito as Requisito } from './requisito';
import { IOferecimento as Oferecimento } from './oferecimento';

export class Curso {
    sigla: string;
    name: string;
    creditos: Credito;
    carga_horaria: number;
    objetivos: string;
    docentes: Docente[];
    programa: string;
    programa_resumido: string;
    avaliacao: Avaliacao;
    bibliografia: string[];
    requisitos: Requisito[];
    oferecimento: Oferecimento[];
}