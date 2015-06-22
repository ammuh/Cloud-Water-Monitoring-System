package com.fluxplant;



import com.google.api.server.spi.config.Api;
import com.google.api.server.spi.config.ApiMethod;
import com.google.api.server.spi.config.ApiMethod.HttpMethod;
import com.google.api.server.spi.response.UnauthorizedException;
import com.google.appengine.api.users.User;
/**
  * Add your first API methods in this class, or you may create another class. In that case, please
  * update your web.xml accordingly.
 **/
@Api(name = "fluxplant", version = "v1", scopes = {Constants.EMAIL_SCOPE },
clientIds = {
	Constants.WEB_CLIENT_ID,
	Constants.API_EXPLORER_CLIENT_ID },
description = "API for the FLux Plant Backend application.")

public class CloudEndpoints {
}
