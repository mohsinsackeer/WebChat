import { configureStore } from "@reduxjs/toolkit";
import globalReducer from "./slices/globalSlice";
import authReducer from "./slices/authSlice";

export const globalstore = configureStore({
  reducer: {
    globalReducer,
    authReducer,
  },
});

export type RootState = ReturnType<typeof globalstore.getState>;
export type GlobalDispatch = typeof globalstore.dispatch;
