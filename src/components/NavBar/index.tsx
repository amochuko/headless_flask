import React from 'react';

import './navbar.module.scss';

import { INavList } from '../../types';

const NavBar: React.FC<INavList> = props => {
	/** Needs props - navMenuList form the nav list */

	console.log('props:', props)
	function getList() {
		for (let res of props.navMenuList) {
			console.log(res);
		}
	}

	return (
		<div>
			<ul>{/* <li key={navMenu.id}>{res.title}</li> */}</ul>
		</div>
	);
};

export default NavBar;
