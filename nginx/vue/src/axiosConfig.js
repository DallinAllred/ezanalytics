import axios from 'axios'

const API_SERVER = 'https://www.ezanalytics.dbaprojects.com'

const axiosInstance = axios.create({
    withCredentials: true,
    baseURL: API_SERVER
})

export default axiosInstance