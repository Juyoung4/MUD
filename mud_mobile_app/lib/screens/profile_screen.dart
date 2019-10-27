import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/models/user_model.dart';
import 'package:mud_mobile_app/services/auth_service.dart';
import 'package:mud_mobile_app/utilities/constants.dart';

class ProfileScreen extends StatefulWidget {

  final String userId;
  ProfileScreen({this.userId});

  @override
  _ProfileScreenState createState() => _ProfileScreenState();
}

  Future<DocumentSnapshot> _getUserData(userId) async {
    return Firestore.instance.collection('users').document(userId).get();
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
    return Scaffold(
      body: AnnotatedRegion<SystemUiOverlayStyle>(
        value: SystemUiOverlayStyle.dark,
        child: CustomScrollView(
          primary: true,
          slivers: <Widget>[
            SliverAppBar(
              expandedHeight: 80.0,
              elevation: 0.0,
              floating: false,
              pinned: true,
              backgroundColor: Color(0xFFFAFAFA),
              flexibleSpace: FlexibleSpaceBar(
                centerTitle: false,
                titlePadding: EdgeInsets.only(left: 16.0, bottom: 8.0),
                title: Text('My Profile', style: myTextStyleDark),
              ),
            ),
            SliverFillRemaining(
              child: FutureBuilder(
                future: _getUserData(widget.userId),
                builder: (BuildContext context, AsyncSnapshot snapshot) {
                  if (!snapshot.hasData) {
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
                                  color: Colors.black12,
                                  blurRadius: 6.0,
                                  offset: Offset(0, 2),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                      Container(
                        padding: EdgeInsets.fromLTRB(4.0, 16.0, 4.0, 4.0),
                        child: Text(user.name, style: myProfileTextStyle,)
                      ),
                      Container(
                        padding: EdgeInsets.all(4.0),
                        child: Text(user.email, style: myProfileTextStyle,)
                      ),
                      SizedBox(
                        height: 100.0,
                      ),
                      _buildProfileEditBtn(),
                      _buildLogOutBtn(context),
                    ],
                  );
                }
              )
            ),
          ],
        ),
      ),
    );
  }
}