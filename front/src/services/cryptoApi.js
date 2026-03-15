import axios from "axios";

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

export const cryptoApi = {
    init: async() =>{
        const response = await api.get('/init');
        return response.data.cartes;
    },

    coder: async(message, paquet) => {
        const response = await api.post('/coder', {
            message: message,
            paquet: paquet
        });
        return response.data;
    },

    decoder: async(code, paquet) => {
        const response = await api.post('/decoder', {
            code: code, 
            paquet: paquet
        });
        return response.data;
    }
}