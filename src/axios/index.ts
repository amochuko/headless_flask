import axios from 'axios'

declare module 'axios' {
  export interface AxiosResponse<T = any> extends Promise<T> {}
}


const instance = axios.create({
	baseURL: 'http://localhost:5000/api',
	timeout: 5000,
	//headers: { 'X-Custom-Header': 'foobar' }
});

instance.defaults.headers.common['Authorization'] = process.env.AUTH_TOKEN;

export default instance