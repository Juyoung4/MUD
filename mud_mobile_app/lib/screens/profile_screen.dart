import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/services/auth_service.dart';
import 'package:mud_mobile_app/utilities/constants.dart';

class ProfileScreen extends StatefulWidget {
  @override
  _ProfileScreenState createState() => _ProfileScreenState();
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
            SliverToBoxAdapter(
              child: Container(
                height: 600,
                child: Center(
                  child: RaisedButton(
                    child: Text("LOGOUT"),
                    onPressed: (){
                      AuthService.logout(context);
                    },
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}