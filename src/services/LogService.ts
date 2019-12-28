export default class LogService {
	constructor() {}

	static logError(err: any) {
		//TODO: implement error post log

		console.log('error.config:', err.config);
		if (err.response) {
			// The request was made and the server responded with a status code
			// that falls out of the range of 2xx
			console.log(err.response);
			throw new Error(err);
		} else if (err.request) {
			// The request was made but no response was received
			console.log(err.request);
			throw new Error(err);
		} else {
			// Something happened in setting up the request that triggered an Error
			console.log(err.message);
			throw new Error(err);
		}
	}
}
