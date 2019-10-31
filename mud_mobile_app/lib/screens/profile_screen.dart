import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/models/user_model.dart';
import 'package:mud_mobile_app/services/auth_service.dart';
import 'package:mud_mobile_app/utilities/constants.dart';
import 'package:mud_mobile_app/utilities/fade_in_animation.dart';

class ProfileScreen extends StatefulWidget {

  @override
  _ProfileScreenState createState() => _ProfileScreenState();
}

  Future<DocumentSnapshot> _getUserData() async {
    FirebaseUser user = await AuthService.getCurrentUser();
    return await Firestore.instance.collection('users').document(user.uid).get();
  }

Widget _buildLogOutBtn(context) {
    return Container(
      padding: EdgeInsets.symmetric(vertical: 25.0, horizontal: 60.0),
      width: double.infinity,
      child: RaisedButton(
        elevation: 2.0,
        onPressed: () {
          AuthService.logout(context);
        },
        padding: EdgeInsets.all(15.0),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30.0),
        ),
        color: Colors.white,
        child: Text(
          'LOGOUT',
          style: TextStyle(
            color: Color(0xFF73AEF5),
            letterSpacing: 1.5,
            fontSize: 18.0,
            fontWeight: FontWeight.bold,
            fontFamily: 'OpenSans',
          ),
        ),
      ),
    );
  }

  Widget _buildProfileEditBtn() {
    return Container(
      padding: EdgeInsets.symmetric(vertical: 25.0, horizontal: 60.0),
      width: double.infinity,
      child: RaisedButton(
        elevation: 2.0,
        onPressed: () {
          print('Edit Pressed!');
        },
        padding: EdgeInsets.all(15.0),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30.0),
        ),
        color: Colors.white,
        child: Text(
          'EDIT PROFILE',
          style: TextStyle(
            color: Color(0xFF73AEF5),
            letterSpacing: 1.5,
            fontSize: 18.0,
            fontWeight: FontWeight.bold,
            fontFamily: 'OpenSans',
          ),
        ),
      ),
    );
  }

class _ProfileScreenState extends State<ProfileScreen> {
  @override
  Widget build(BuildContext context) {
    final double devHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      backgroundColor: Colors.white,
      body: AnnotatedRegion<SystemUiOverlayStyle>(
        value: SystemUiOverlayStyle.dark,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Container(
              padding: EdgeInsets.only(bottom: 10.0),
              height: (devHeight / 2) * 0.4,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: <Widget>[
                  Column(
                    mainAxisAlignment: MainAxisAlignment.end,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: <Widget>[
                      Container(
                        child: FadeIn(1.0, Text("Today's News", style: kTopBarTitleStyle)),
                      ),
                      Container(
                        child: FadeIn(1.3, Text("Profile", style: kTopBarTitleStyle)),
                      ),
                    ],
                  ),
                  FadeIn(1.6, Container(
                    height: (devHeight / 2) * 0.2,
                    child: Image.asset('assets/images/profile.png'),
                    decoration: BoxDecoration(
                      boxShadow: [
                        BoxShadow(
                          color: Colors.greenAccent.withOpacity(0.3),
                          blurRadius: 20.0,
                          spreadRadius: 5.0,
                          offset: Offset(5.0, 5.0)
                        )
                      ]
                    ),
                  ))
                ],
              ),
            ),
            Expanded(
              child: FutureBuilder(
                future: _getUserData(),
                builder: (BuildContext context, AsyncSnapshot snapshot) {
                  if (snapshot.data == null) {
                    return Padding(
                      padding: const EdgeInsets.all(50.0),
                      child: Center(
                        child: CircularProgressIndicator(),
                      ),
                    );
                  }
                  User user = User.fromDoc(snapshot.data);
                  return Column(
                    children: <Widget>[
                      Padding(
                        padding: const EdgeInsets.only(top: 60),
                        child: Center(
                          child: Container(
                            child: CircleAvatar(
                              backgroundImage: NetworkImage('https://bukiya.lk/upload/photos/2018/04/Ra8foNy1ki56SDiH4Oux_19_defe1f0b9a8471a31b17036dd1009bce_avatar_full.jpg'),
                            ),
                            width: 100,
                            height: 100,
                            padding: EdgeInsets.all(2.0),
                            decoration: BoxDecoration(
                              color: Color(0xFF73AEF5),
                              shape: BoxShape.circle,
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.blueAccent.withOpacity(0.3),
                                  blurRadius: 20.0,
                                  spreadRadius: 5.0,
                                  offset: Offset.zero
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                      Container(
                        padding: EdgeInsets.fromLTRB(4.0, 16.0, 4.0, 4.0),
                        child: Text(
                          user.name,
                          style: TextStyle(
                            color: Colors.black45,
                            fontFamily: 'OpenSans',
                            fontSize: 20.0,
                            letterSpacing: 1.5,
                            fontWeight: FontWeight.bold,
                          ),
                        )
                      ),
                      Container(
                        padding: EdgeInsets.all(4.0),
                        child: Text(
                          user.email,
                          style: TextStyle(
                            color: Colors.black45,
                            fontFamily: 'OpenSans',
                            fontSize: 20.0,
                            letterSpacing: 1.5,
                            fontWeight: FontWeight.bold,
                          ),
                        )
                      ),
                      SizedBox(
                        height: 50.0,
                      ),
                      _buildProfileEditBtn(),
                      _buildLogOutBtn(context),
                    ],
                  );
                }
              )
            )
          ],
        )
      ),
    );
  }
}