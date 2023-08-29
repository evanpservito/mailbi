import { useContext, createContext, useState, useEffect } from "react";
import {
  GoogleAuthProvider,
  signInWithRedirect,
  signOut,
  onAuthStateChanged,
} from "firebase/auth";
import { auth } from "../Firebase";
// import firebase from "../Firebase";
// import { onSnapshot, collection, query, where } from "firebase/firestore";

const AuthContext = createContext<any>(null);

export const AuthContextProvider = ({ children }: any) => {
  const [user, setUser] = useState({});
  //const [authorizedUsers, setAuthorizedUsers] = useState({});

  // ensure user is authorized before accessing tracking log
  // const getAuthorizedEmails = () => {
  //   const q = query(collection(firebase, "allow-users"));
  //   const unsub = onSnapshot(q, (querySnapshot: any) => {
  //     const items: any[] = [];
  //     querySnapshot.forEach((doc: any) => {
  //       items.push(doc.data()["email"]);
  //     });
  //     setAuthorizedUsers(items);
  //   });
  //   return () => {
  //     unsub();
  //   };
  // };

  const googleLogin = () => {
    const provider = new GoogleAuthProvider();
    signInWithRedirect(auth, provider);
  };

  const logOut = () => {
    signOut(auth);
  };
  useEffect(() => {
    //getAuthorizedEmails();
    const unsubscribe = onAuthStateChanged(auth, (currentUser: any) => {
      // if (currentUser?.email in authorizedUsers == false) {
      //   console.log("unauthorized user", currentUser?.email, authorizedUsers);
      //   logOut();
      // }
      setUser(currentUser);
      // console.log("user: ", currentUser);
    });
    return () => {
      unsubscribe();
    };
  }, []);
  return (
    <AuthContext.Provider value={{ googleLogin, logOut, user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const UserAuth = () => {
  return useContext(AuthContext);
};
