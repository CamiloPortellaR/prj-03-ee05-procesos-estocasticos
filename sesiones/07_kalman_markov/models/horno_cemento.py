"""Simulación y filtro de Kalman — alimentación de materia prima en horno de cemento."""

from dataclasses import dataclass

import numpy as np

# Parámetros compartidos (artículo de referencia en docs/casos_industriales/)
SEED_CASO1 = 42
SEED_CASO2 = 42
SETPOINT_CONST = 375.0
PROCESS_SIGMA = 0.05
MEASUREMENT_SIGMA = 1.5
N_SAMPLES_CASO1 = 500
N_SAMPLES_CASO2 = 800
Q_PROCESO = 0.01
P_INICIAL = 1.2
A_ESTADO = 1.0
H_MEDICION = 1.0


@dataclass(frozen=True)
class DatosCaso1:
    caudal_verdadero: np.ndarray
    medicion: np.ndarray
    setpoint: float
    sigma_medicion: float


@dataclass(frozen=True)
class DatosCaso2:
    caudal_verdadero: np.ndarray
    medicion: np.ndarray
    setpoint: np.ndarray
    sigma_medicion: float


@dataclass(frozen=True)
class ResultadoKalman:
    estimacion: np.ndarray
    covarianza: np.ndarray


def simular_setpoint_constante() -> DatosCaso1:
    """Caso 1: setpoint fijo con medición ruidosa."""
    rng = np.random.default_rng(SEED_CASO1)
    n = N_SAMPLES_CASO1
    caudal = np.zeros(n)
    caudal[0] = SETPOINT_CONST

    for k in range(1, n):
        caudal[k] = caudal[k - 1] + rng.normal(0, PROCESS_SIGMA)

    medicion = caudal + rng.normal(0, MEASUREMENT_SIGMA, size=n)
    return DatosCaso1(caudal, medicion, SETPOINT_CONST, MEASUREMENT_SIGMA)


def simular_setpoint_variable() -> DatosCaso2:
    """Caso 2: setpoint escalonado con medición ruidosa."""
    rng = np.random.default_rng(SEED_CASO2)
    n = N_SAMPLES_CASO2
    setpoint = np.zeros(n)
    setpoint[:200] = 370.0
    setpoint[200:400] = 375.0
    setpoint[400:600] = 380.0
    setpoint[600:] = 385.0

    caudal = np.zeros(n)
    caudal[0] = setpoint[0]

    for k in range(1, n):
        deriva = (setpoint[k] - caudal[k - 1]) * 0.1
        caudal[k] = caudal[k - 1] + deriva + rng.normal(0, PROCESS_SIGMA)

    medicion = caudal + rng.normal(0, MEASUREMENT_SIGMA, size=n)
    return DatosCaso2(caudal, medicion, setpoint, MEASUREMENT_SIGMA)


def filtro_kalman_escalar(
    medicion: np.ndarray,
    setpoint_inicial: float,
    sigma_medicion: float,
    q_proceso: float = Q_PROCESO,
    p_inicial: float = P_INICIAL,
) -> ResultadoKalman:
    """Filtro de Kalman escalar: X(k)=X(k-1)+W, Z(k)=X(k)+V."""
    n = len(medicion)
    x_est = np.zeros(n)
    p_est = np.zeros(n)
    x_est[0] = setpoint_inicial
    p_est[0] = p_inicial
    ruido_medicion = sigma_medicion**2

    for k in range(1, n):
        x_pred = A_ESTADO * x_est[k - 1]
        p_pred = p_est[k - 1] + q_proceso
        ganancia = p_pred / (p_pred + ruido_medicion)
        x_est[k] = x_pred + ganancia * (medicion[k] - H_MEDICION * x_pred)
        p_est[k] = (1 - ganancia) * p_pred

    return ResultadoKalman(x_est, p_est)


def filtro_kalman_con_reinicio_setpoint(
    medicion: np.ndarray,
    setpoint: np.ndarray,
    sigma_medicion: float,
    q_proceso: float = Q_PROCESO,
    p_inicial: float = P_INICIAL,
) -> ResultadoKalman:
    """Kalman con reinicialización cuando cambia el setpoint (como en el artículo)."""
    n = len(medicion)
    x_est = np.zeros(n)
    p_est = np.zeros(n)
    x_est[0] = setpoint[0]
    p_est[0] = p_inicial
    ruido_medicion = sigma_medicion**2

    for k in range(1, n):
        if setpoint[k] != setpoint[k - 1]:
            x_est[k - 1] = setpoint[k - 1]
            p_est[k - 1] = p_inicial

        x_pred = A_ESTADO * x_est[k - 1]
        p_pred = p_est[k - 1] + q_proceso
        ganancia = p_pred / (p_pred + ruido_medicion)
        x_est[k] = x_pred + ganancia * (medicion[k] - H_MEDICION * x_pred)
        p_est[k] = (1 - ganancia) * p_pred

    return ResultadoKalman(x_est, p_est)
