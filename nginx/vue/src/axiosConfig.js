import axios from 'axios'

const API_SERVER = import.meta.env.VITE_API_SERVER

const axiosInstance = axios.create({
    withCredentials: true,
    baseURL: API_SERVER
})

export default axiosInstance