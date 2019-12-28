import ErrorService from '../services/LogService';

export function logError(err: any):void {
    /** send to error service  */
    ErrorService.logError(err);
}
