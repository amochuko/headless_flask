import axios from '../axios';

import { logError } from '../util/logError';

class NavMenu {
	static async getNavMenuList() {
		try {
			const navMenu = await axios.get('/nav/');
			if (navMenu.status === 200) {
				return navMenu.data;
			}
		} catch (err) {
			logError(err);
		}
	}
}

export default NavMenu;
