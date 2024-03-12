import axios from 'axios'

const API_SERVER = 'http://lvh.me:5050'

const axiosInstance = axios.create({
    withCredentials: true,
    baseURL: API_SERVER,
    validateStatus: () => true
})

export default axiosInstance