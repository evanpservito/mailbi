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

  // // if error occurs, then user is not authorized; TODO: update later
  // const getAuthorizedEmails = () => {
  //   try {
  //     const q = query(collection(firebase, "allow-users"));
  //     const unsub = onSnapshot(q, (querySnapshot: any) => {
  //       const items: any[] = [];
  //       querySnapshot.forEach((doc: any) => {
  //         items.push(doc.data()["email"]);
  //       });
  //     });
  //   } catch {
  //     console.log("unauthorized user");
  //     // logOut();
  //   }
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
    const unsubscribe = onAuthStateChanged(auth, (currentUser: any) => {
      // try {
      //   getAuthorizedEmails();
      // } catch {
      //   console.log("unauthorized user");
      //   // logOut();
      // }
      setUser(currentUser);
      console.log("user: ", currentUser);
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
