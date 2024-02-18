"use client";

import React, { ReactNode } from "react";
import { Provider } from "react-redux";
import { globalstore } from "./store";

type Props = {
  children: ReactNode;
};

const GlobalProvider: React.FC<Props> = ({ children }) => {
  return <Provider store={globalstore}>{children}</Provider>;
};

export default GlobalProvider;
