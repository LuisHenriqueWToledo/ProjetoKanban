from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from database import get_db
import models
import schemas

router = APIRouter(tags=["Raias"])


def _quadro_ou_404(codigo_quadro: str, db: Session) -> models.Quadro:
    quadro = db.query(models.Quadro).filter(models.Quadro.codigo == codigo_quadro).first()
    if not quadro:
        raise HTTPException(status_code=404, detail="Quadro nao encontrado")
    return quadro


@router.post("/quadros/{codigo_quadro}/raias", response_model=schemas.RaiaOut, status_code=status.HTTP_201_CREATED)
def criar_raia(codigo_quadro: str, payload: schemas.RaiaCreate, db: Session = Depends(get_db)):
    _quadro_ou_404(codigo_quadro, db)

    raia = models.Raia(
        codigo_quadro=codigo_quadro,
        nome=payload.nome,
        responsavel=payload.responsavel,
        ordem_exibicao=payload.ordem_exibicao,
    )
    db.add(raia)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ja existe uma raia com este nome no quadro")
    db.refresh(raia)
    return raia


@router.get("/quadros/{codigo_quadro}/raias", response_model=List[schemas.RaiaOut])
def listar_raias(codigo_quadro: str, db: Session = Depends(get_db)):
    _quadro_ou_404(codigo_quadro, db)
    return db.query(models.Raia).filter(
        models.Raia.codigo_quadro == codigo_quadro
    ).order_by(models.Raia.ordem_exibicao.asc(), models.Raia.id_raia.asc()).all()


@router.put("/raias/{id_raia}", response_model=schemas.RaiaOut)
def editar_raia(id_raia: int, payload: schemas.RaiaUpdate, db: Session = Depends(get_db)):
    raia = db.query(models.Raia).filter(models.Raia.id_raia == id_raia).first()
    if not raia:
        raise HTTPException(status_code=404, detail="Raia nao encontrada")

    raia.nome = payload.nome
    raia.responsavel = payload.responsavel
    raia.ordem_exibicao = payload.ordem_exibicao
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ja existe uma raia com este nome no quadro")

    # Mantem consistencia visual entre raia e cartoes associados.
    db.query(models.Cartao).filter(models.Cartao.id_raia == id_raia).update(
        {models.Cartao.responsavel: payload.responsavel},
        synchronize_session=False,
    )
    db.commit()
    db.refresh(raia)
    return raia


@router.delete("/raias/{id_raia}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_raia(id_raia: int, db: Session = Depends(get_db)):
    raia = db.query(models.Raia).filter(models.Raia.id_raia == id_raia).first()
    if not raia:
        raise HTTPException(status_code=404, detail="Raia nao encontrada")

    tem_cartoes = db.query(models.Cartao).filter(models.Cartao.id_raia == id_raia).count() > 0
    if tem_cartoes:
        raise HTTPException(status_code=409, detail="Existem cartoes vinculados a esta raia; realoque-os antes de excluir")

    db.delete(raia)
    db.commit()
