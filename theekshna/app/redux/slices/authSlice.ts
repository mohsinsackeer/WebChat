import { TAuthState } from "@/app/intefaces/global";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";
export const initialState: TAuthState = {
  accessToken: undefined,
};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setAccessToken: (state, action: PayloadAction<string>) => {
      return {
        accessToken: action.payload,
      };
    },
  },
});

export const { setAccessToken } = authSlice.actions;
export default authSlice.reducer;
