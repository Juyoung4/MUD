import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/screens/login_screen.dart';
import 'package:mud_mobile_app/screens/signup_screen.dart';
import 'package:mud_mobile_app/services/auth_service.dart';
import 'package:mud_mobile_app/utilities/constants.dart';
import 'package:mud_mobile_app/utilities/fade_in_animation.dart';

class ErrorScreen extends StatefulWidget {
  static final String id = 'error_screen';
  @override
  _ErrorScreenState createState() => _ErrorScreenState();
}

Widget _buildBackBtn(context) {
    return Container(
      padding: EdgeInsets.symmetric(vertical: 25.0),
      width: double.infinity,
      child: RaisedButton(
        elevation: 5.0,
        onPressed: () {
          if (AuthService.getAuthRoutes() == 'signUp') {
            Navigator.pushReplacementNamed(context, SignUpScreen.id);
          } else {
            Navigator.pushReplacementNamed(context, LoginScreen.id);
          }
        },
        padding: EdgeInsets.all(15.0),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30.0),
        ),
        color: Colors.white,
        child: Text(
          'GO BACK',
          style: TextStyle(
            color: Color(0xFF527DAA),
            letterSpacing: 1.5,
            fontSize: 18.0,
            fontWeight: FontWeight.bold,
            fontFamily: 'OpenSans',
          ),
        ),
      ),
    );
  }


class _ErrorScreenState extends State<ErrorScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AnnotatedRegion<SystemUiOverlayStyle>(
        value: SystemUiOverlayStyle.light,
        child: GestureDetector(
          onTap: () => FocusScope.of(context).unfocus(),
          child: Stack(
            children: <Widget>[
              Container(
                height: double.infinity,
                width: double.infinity,
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: bacgroundColors,
                    stops: [0.1, 0.4, 0.7, 0.9],
                  ),
                ),
              ),
              Container(
                height: double.infinity,
                child: SingleChildScrollView(
                  physics: AlwaysScrollableScrollPhysics(),
                  padding: EdgeInsets.symmetric(
                    horizontal: 40.0,
                    vertical: 120.0,
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: <Widget>[
                      FadeIn(1.0, Text(
                        'News App',
                        style: kTitleStyle
                      )),
                      SizedBox(height: 20.0),
                      FadeIn(1.3, Text(
                        'You Got an Error!',
                        style: TextStyle(
                          color: Colors.white,
                          fontFamily: 'OpenSans',
                          fontSize: 26.0,
                          fontWeight: FontWeight.bold,
                        ),
                      )),
                      SizedBox(height: 20.0),
                      FadeIn(1.6, Container(
                        height: 200,
                        decoration: BoxDecoration(
                          shape: BoxShape.rectangle
                        ),
                        child: Image.asset('assets/images/sad.png'),
                      )),
                      SizedBox(height: 10.0),
                      FadeIn(1.9, Text(
                        AuthService.getError(),
                        style: TextStyle(
                          color: Colors.white,
                          fontFamily: 'OpenSans',
                          fontSize: 18.0,
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                      )),
                      SizedBox(height: 10.0),
                      FadeIn(2.2, _buildBackBtn(context)),
                    ],
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}