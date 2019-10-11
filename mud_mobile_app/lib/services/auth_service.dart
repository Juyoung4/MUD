import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:mud_mobile_app/screens/home_screen.dart';
import 'package:mud_mobile_app/screens/login_screen.dart';

class AuthService {
  static final _auth = FirebaseAuth.instance;
  static final _firestore = Firestore.instance;

  static Future signUpUser(BuildContext context, String name, String email, String password) async {
    try {
      AuthResult authResult = await _auth.createUserWithEmailAndPassword(
        email:  email,
        password: password,
      );
      FirebaseUser signedInUser = authResult.user;
      if (signedInUser != null) {
        _firestore.collection('/users').document(signedInUser.uid).setData({
          'name': name,
          'email': email,
          'profileImageUrl': '',
        });
        Navigator.pushReplacementNamed(context, HomeScreen.id);
      }
    } catch (e) {
      print(e);
    }
  }

  static void logout(BuildContext context) {
    _auth.signOut();
    Navigator.pushReplacementNamed(context, LoginScreen.id);
  }

  static void login(BuildContext context, String email, String password) async {
    try {
      await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
      Navigator.pushReplacementNamed(context, HomeScreen.id);
    } catch (e) {
      print(e);
    }
  }
}