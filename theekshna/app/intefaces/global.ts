export interface TAction {
  type: string;
  payload: string | undefined;
}

export interface TGlobalState {
  selectedChat: string | undefined;
}

export interface TAuthState {
  accessToken: string | undefined;
}
