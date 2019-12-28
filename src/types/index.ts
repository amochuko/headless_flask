export interface IState {
  navMenuList: Array<{ id: string; title: string }>;
  error? : string;
}

export interface INavList {
	navMenuList: Array<{ id: string; title: string }>;
}
