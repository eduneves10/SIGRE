import api from './api'

/**
 * Lista as salas - GET /rooms/
 * Retorna: [{id, codigo_sala, descricao_sala,...}]
 */

export const getRooms = async () => {
    const res = await api.get('/rooms/')
    return res.data
}