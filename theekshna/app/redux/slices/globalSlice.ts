import { PayloadAction, createSlice } from "@reduxjs/toolkit";
import { TGlobalState } from "@/app/intefaces/global";

const initialState: TGlobalState = {
  selectedChat: undefined,
};
const globalSlice = createSlice({
  name: "global",
  initialState,
  reducers: {
    setSelectedChat: (state, action: PayloadAction<string>) => {
      state.selectedChat = action.payload;
    },
  },
});

export const { setSelectedChat } = globalSlice.actions;
export default globalSlice.reducer;
