import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/models/Conection_error.dart';
import 'package:mud_mobile_app/models/user_model.dart';
import 'package:mud_mobile_app/screens/bookmarks_screen.dart';
import 'package:mud_mobile_app/services/auth_service.dart';
import 'package:mud_mobile_app/utilities/constants.dart';
import 'package:mud_mobile_app/utilities/fade_in_animation.dart';
import 'package:mud_mobile_app/utilities/shape_paint.dart';

class ProfileScreen extends StatefulWidget {

  @override
  _ProfileScreenState createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {

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

  Widget _buildBookmarkBtn(context) {
    return Container(
      padding: EdgeInsets.symmetric(vertical: 25.0, horizontal: 60.0),
      width: double.infinity,
      child: RaisedButton(
        elevation: 2.0,
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => BookmarksPage()),
          );
        },
        padding: EdgeInsets.all(15.0),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30.0),
        ),
        color: Colors.white,
        child: Text(
          'BOOKMARKS',
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


  @override
  Widget build(BuildContext context) {
    final double devHeight = MediaQuery.of(context).size.height;
    final double devWidth = MediaQuery.of(context).size.width;
    return Scaffold(
      backgroundColor: Colors.white,
      body: AnnotatedRegion<SystemUiOverlayStyle>(
        value: SystemUiOverlayStyle.dark,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Stack(
              children: <Widget>[
                CustomPaint(
                  painter: Chevron(),
                  child: Container(
                    height: devHeight * 0.2,
                    width: devWidth,
                    child: Padding(
                      padding: EdgeInsets.symmetric(horizontal: 20),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: <Widget>[
                          IconButton(
                            color: Colors.transparent,
                            icon: Icon(Icons.arrow_back_ios, size: 36,),
                            onPressed: (){},
                          ),
                          Text('My Profile', style: kTitleStyleMain,),
                          IconButton(
                            color: Colors.white,
                            icon: Icon(Icons.search, size: 36,),
                            onPressed: (){},
                          ),
                        ],
                      ),
                    )
                  ),
                )
              ],
            ),
            Expanded(
              child: SingleChildScrollView(
                child: FutureBuilder(
                  future: _getUserData(),
                  builder: (BuildContext context, AsyncSnapshot snapshot) {
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return Padding(
                        padding: const EdgeInsets.all(50.0),
                        child: Center(
                          child: CircularProgressIndicator(),
                        ),
                      );
                    } else if (snapshot.hasError || !snapshot.hasData) {
                      return Center(
                        child: ErrorDisplay(errorDisplay: 'Error Loading Profile Data', error: false,),
                      );
                    }
                    User user = User.fromDoc(snapshot.data);
                    return FadeIn(1.6, Column(
                      children: <Widget>[
                        Padding(
                          padding: const EdgeInsets.only(top: 60),
                          child: Center(
                            child: Container(
                              child: CircleAvatar(
                                backgroundImage: AssetImage('assets/images/avatar.png'),
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
                          height: 30.0,
                        ),
                        _buildBookmarkBtn(context),
                        _buildLogOutBtn(context),
                      ],
                    ));
                  }
                ),
              )
            )
          ],
        )
      ),
    );
  }
}