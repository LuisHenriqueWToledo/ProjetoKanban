from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import datetime, timedelta
from database import get_db
import models
import schemas

router = APIRouter(prefix="/cartoes", tags=["Cartões"])


def _recalcular_status_quadro(codigo_quadro: str, db: Session):
    """Atualiza o status do quadro automaticamente com base nas colunas dos seus cartões."""
    quadro = db.query(models.Quadro).filter(models.Quadro.codigo == codigo_quadro).first()
    if not quadro:
        return
    cartoes = db.query(models.Cartao).filter(models.Cartao.codigo_quadro == codigo_quadro).all()
    if not cartoes:
        return
    colunas = [c.coluna for c in cartoes]
    if all(col == "FEITO" for col in colunas):
        quadro.status = "CONCLUIDO"
    elif all(col in ("FEITO", "EM TESTE") for col in colunas):
        quadro.status = "EM TESTES"
    elif all(col == "A FAZER" for col in colunas):
        quadro.status = "A FAZER"
    else:
        quadro.status = "EM ANDAMENTO"
    db.commit()


@router.post("/", response_model=schemas.CartaoOut, status_code=status.HTTP_201_CREATED)
def criar_cartao(payload: schemas.CartaoCreate, db: Session = Depends(get_db)):
    quadro = db.query(models.Quadro).filter(models.Quadro.codigo == payload.codigo_quadro).first()
    if not quadro:
        raise HTTPException(status_code=404, detail="Quadro não encontrado")

    raia = db.query(models.Raia).filter(
        models.Raia.id_raia == payload.id_raia,
        models.Raia.codigo_quadro == payload.codigo_quadro,
    ).first()
    if not raia:
        raise HTTPException(status_code=404, detail="Raia nao encontrada para o quadro informado")

    existente = db.query(models.Cartao).filter(
        models.Cartao.codigo == payload.codigo,
        models.Cartao.codigo_quadro == payload.codigo_quadro,
    ).first()
    if existente:
        raise HTTPException(status_code=409, detail="Código de cartão já existe neste quadro")

    cartao = models.Cartao(
        codigo=payload.codigo,
        codigo_quadro=payload.codigo_quadro,
        id_raia=payload.id_raia,
        nome=payload.nome,
        descricao=payload.descricao,
        responsavel=raia.responsavel,
        prioridade=payload.prioridade.value,
        data_limite=payload.data_limite,
        coluna=payload.coluna.value,
    )
    db.add(cartao)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Código de cartão já existe")
    db.refresh(cartao)
    _recalcular_status_quadro(cartao.codigo_quadro, db)
    return cartao


@router.get("/quadro/{codigo_quadro}", response_model=List[schemas.CartaoOut])
def listar_cartoes(codigo_quadro: str, db: Session = Depends(get_db)):
    return db.query(models.Cartao).filter(models.Cartao.codigo_quadro == codigo_quadro).all()


@router.get("/{codigo}", response_model=schemas.CartaoOut)
def visualizar_cartao(codigo: str, codigo_quadro: str = Query(...), db: Session = Depends(get_db)):
    cartao = db.query(models.Cartao).filter(
        models.Cartao.codigo == codigo,
        models.Cartao.codigo_quadro == codigo_quadro,
    ).first()
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    return cartao


@router.patch("/{codigo}/mover", response_model=schemas.CartaoOut)
def mover_cartao(codigo: str, payload: schemas.CartaoMover, codigo_quadro: str = Query(...), db: Session = Depends(get_db)):
    cartao = db.query(models.Cartao).filter(
        models.Cartao.codigo == codigo,
        models.Cartao.codigo_quadro == codigo_quadro,
    ).first()
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")

    quadro = db.query(models.Quadro).filter(models.Quadro.codigo == codigo_quadro).first()

    agora = datetime.utcnow()
    nova_coluna = payload.coluna.value

    # O limite WIP só vale para colunas de trabalho em andamento.
    if nova_coluna in ("FAZENDO", "EM TESTE"):
        qtd_coluna = db.query(models.Cartao).filter(
            models.Cartao.codigo_quadro == cartao.codigo_quadro,
            models.Cartao.coluna == nova_coluna,
            models.Cartao.codigo != codigo,
        ).count()
        if qtd_coluna >= quadro.limite_wip:
            raise HTTPException(status_code=409, detail=f"Limite WIP atingido na coluna '{nova_coluna}'")

    # Registrar timestamps de ciclo
    if nova_coluna == "FAZENDO" and cartao.iniciado_em is None:
        cartao.iniciado_em = agora
    if nova_coluna == "FEITO" and cartao.concluido_em is None:
        cartao.concluido_em = agora

    cartao.coluna = nova_coluna
    db.commit()
    db.refresh(cartao)
    _recalcular_status_quadro(cartao.codigo_quadro, db)
    return cartao


@router.patch("/{codigo}/mover-raia", response_model=schemas.CartaoOut)
def mover_cartao_raia(
    codigo: str,
    payload: schemas.CartaoMoverRaia,
    codigo_quadro: str = Query(...),
    db: Session = Depends(get_db),
):
    cartao = db.query(models.Cartao).filter(
        models.Cartao.codigo == codigo,
        models.Cartao.codigo_quadro == codigo_quadro,
    ).first()
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartao nao encontrado")

    raia_destino = db.query(models.Raia).filter(
        models.Raia.id_raia == payload.id_raia,
        models.Raia.codigo_quadro == codigo_quadro,
    ).first()
    if not raia_destino:
        raise HTTPException(status_code=404, detail="Raia de destino nao encontrada no quadro")

    cartao.id_raia = raia_destino.id_raia
    cartao.responsavel = raia_destino.responsavel
    db.commit()
    db.refresh(cartao)
    return cartao


@router.put("/{codigo}", response_model=schemas.CartaoOut)
def editar_cartao(codigo: str, payload: schemas.CartaoUpdate, codigo_quadro: str = Query(...), db: Session = Depends(get_db)):
    cartao = db.query(models.Cartao).filter(
        models.Cartao.codigo == codigo,
        models.Cartao.codigo_quadro == codigo_quadro,
    ).first()
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    cartao.nome = payload.nome
    cartao.descricao = payload.descricao
    cartao.responsavel = payload.responsavel
    cartao.prioridade = payload.prioridade.value
    cartao.data_limite = payload.data_limite
    db.commit()
    db.refresh(cartao)
    return cartao


@router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_cartao(codigo: str, codigo_quadro: str = Query(...), db: Session = Depends(get_db)):
    cartao = db.query(models.Cartao).filter(
        models.Cartao.codigo == codigo,
        models.Cartao.codigo_quadro == codigo_quadro,
    ).first()
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    db.delete(cartao)
    db.commit()
    _recalcular_status_quadro(codigo_quadro, db)


@router.get("/quadro/{codigo_quadro}/metricas", response_model=schemas.MetricasOut)
def metricas(codigo_quadro: str, db: Session = Depends(get_db)):
    todos = db.query(models.Cartao).filter(models.Cartao.codigo_quadro == codigo_quadro).all()

    wip_atual = sum(1 for c in todos if c.coluna == "FAZENDO")
    agora = datetime.utcnow()
    inicio_janela = agora - timedelta(days=7)
    throughput_7d = sum(
        1 for c in todos
        if c.concluido_em is not None and inicio_janela <= c.concluido_em <= agora
    )

    concluidos = [c for c in todos if c.criado_em and c.concluido_em]
    lead_time = None
    if concluidos:
        lead_time = sum((c.concluido_em - c.criado_em).days for c in concluidos) / len(concluidos)

    ciclo = [c for c in todos if c.iniciado_em and c.concluido_em]
    cycle_time = None
    if ciclo:
        cycle_time = sum((c.concluido_em - c.iniciado_em).days for c in ciclo) / len(ciclo)

    return schemas.MetricasOut(
        wip_atual=wip_atual,
        throughput_7d=throughput_7d,
        throughput_dia_medio=throughput_7d / 7,
        lead_time_medio_dias=lead_time,
        cycle_time_medio_dias=cycle_time,
    )
