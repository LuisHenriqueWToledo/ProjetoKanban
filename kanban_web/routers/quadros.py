from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from database import get_db
import models
import schemas

router = APIRouter(prefix="/quadros", tags=["Quadros"])


@router.post("/", response_model=schemas.QuadroOut, status_code=status.HTTP_201_CREATED)
def criar_quadro(payload: schemas.QuadroCreate, email_dono: str = Query(...), db: Session = Depends(get_db)):
    conta = db.query(models.Conta).filter(models.Conta.email == email_dono).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    existente = db.query(models.Quadro).filter(models.Quadro.codigo == payload.codigo).first()
    if existente:
        raise HTTPException(status_code=409, detail="Código de quadro já existe")
    quadro = models.Quadro(
        codigo=payload.codigo,
        nome=payload.nome,
        descricao=payload.descricao,
        limite_wip=payload.limite_wip,
        email_dono=email_dono,
    )
    db.add(quadro)
    db.commit()
    db.refresh(quadro)
    return quadro


@router.get("/", response_model=List[schemas.QuadroOut])
def listar_quadros(email_dono: str = Query(...), db: Session = Depends(get_db)):
    # Quadros onde é dono
    como_dono = db.query(models.Quadro).filter(models.Quadro.email_dono == email_dono)
    # Quadros onde é membro convidado
    codigos_membro = db.query(models.QuadroMembro.codigo_quadro).filter(
        models.QuadroMembro.email_usuario == email_dono
    ).subquery()
    como_membro = db.query(models.Quadro).filter(models.Quadro.codigo.in_(codigos_membro))
    # União sem duplicatas
    todos = {q.codigo: q for q in como_dono.all() + como_membro.all()}
    return list(todos.values())


@router.get("/{codigo}", response_model=schemas.QuadroOut)
def visualizar_quadro(codigo: str, db: Session = Depends(get_db)):
    quadro = db.query(models.Quadro).filter(models.Quadro.codigo == codigo).first()
    if not quadro:
        raise HTTPException(status_code=404, detail="Quadro não encontrado")
    return quadro


@router.put("/{codigo}", response_model=schemas.QuadroOut)
def atualizar_quadro(codigo: str, payload: schemas.QuadroUpdate, email_dono: str = Query(...), db: Session = Depends(get_db)):
    quadro = db.query(models.Quadro).filter(models.Quadro.codigo == codigo).first()
    if not quadro:
        raise HTTPException(status_code=404, detail="Quadro não encontrado")
    if quadro.email_dono != email_dono:
        raise HTTPException(status_code=403, detail="Sem permissão para editar este quadro")

    quantidade_cartoes = db.query(models.Cartao).filter(models.Cartao.codigo_quadro == codigo).count()
    if quantidade_cartoes > payload.limite_wip:
        raise HTTPException(status_code=409, detail="O limite WIP não pode ser menor que a quantidade atual de cartões")

    quadro.nome = payload.nome
    quadro.descricao = payload.descricao
    quadro.limite_wip = payload.limite_wip
    db.commit()
    db.refresh(quadro)
    return quadro


@router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_quadro(codigo: str, email_dono: str = Query(...), db: Session = Depends(get_db)):
    quadro = db.query(models.Quadro).filter(models.Quadro.codigo == codigo).first()
    if not quadro:
        raise HTTPException(status_code=404, detail="Quadro não encontrado")
    if quadro.email_dono != email_dono:
        raise HTTPException(status_code=403, detail="Sem permissão para excluir este quadro")
    db.delete(quadro)
    db.commit()


@router.patch("/{codigo}/status", response_model=schemas.QuadroOut)
def mover_quadro(codigo: str, payload: schemas.QuadroMoverStatus, db: Session = Depends(get_db)):
    quadro = db.query(models.Quadro).filter(models.Quadro.codigo == codigo).first()
    if not quadro:
        raise HTTPException(status_code=404, detail="Quadro não encontrado")
    quadro.status = payload.status.value
    db.commit()
    db.refresh(quadro)
    return quadro
