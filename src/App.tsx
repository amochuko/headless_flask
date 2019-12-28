import React from 'react';
import logo from './static/img/logo.svg';
import './App.scss';


import NavBar from './components/NavBar';
import NavMenuService from './services/NavMenuService'
import {IState} from './types'

class App extends React.Component {
	state: IState = {
		error: '',
		navMenuList: []
	};

	componentDidMount() {
		document.title = `Headless CMS`;

		NavMenuService.getNavMenuList().then(res => {
			this.setState({ navMenuList: [...res.data] });
		});
	}

	componentDidUpdate() {}

	render() {
		return (
			<div className='App'>
				<header className='App-header'>
					<img src={logo} className='App-logo' alt='logo' />
				</header>
				<NavBar navMenuList={this.state.navMenuList} />
			</div>
		);
	}
}

export default App;
