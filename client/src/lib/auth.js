import { Auth } from '@zalter/identity-js';

const noop = () => {};

export const ENABLE_AUTH = process.env.NEXT_PUBLIC_ENABLE_ZALTER_AUTH === 'true';

// export const auth = ENABLE_AUTH
//   ? new Auth({
//     projectId: process.env.NEXT_PUBLIC_ZALTER_PROJECT_ID
//   })
//   : noop();

export const auth = () => {
  const key = "token";
  const token = localStorage.getItem(key);
  if (token){
    return token;
  }
  return undefined;

}


export const getUserData = () => {
  const key = "userData";
  const userData = JSON.parse(localStorage.getItem(key));
  if (userData){
    return userData;
  }
  return undefined;

}

