import axios from 'axios'

const axiosGh = axios.create({
        baseURL: 'https://api.github.com'
})

export default axiosGh
