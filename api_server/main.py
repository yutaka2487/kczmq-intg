from fastapi import FastAPI, Request, Response
from keycloak import KeycloakOpenID
 
app = FastAPI()

@app.post("/hello")
async def hello():
    """　APIの本体 """
    return {"message":"Hello World"}

@app.middleware("http")
async def auth(request: Request, call_next):
    """ 認証・認可用のミドルウェア """
    try:
        # 認証＋アクセストークン取得
        keycloak_openid = KeycloakOpenID(
            server_url = "http://keycloak:8080/auth/",
            realm_name = "kczmq-intg",
            client_id = request.headers["X-Client-Id"],
            client_secret_key = request.headers["X-Client-Secret-Key"],
        )
        token = keycloak_openid.token(grant_type=["client_credentials"]) 

        #トークンのデコード
        public_key = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
        options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}
        token_info = keycloak_openid.decode_token(token['access_token'], key=public_key, options=options)

        # TODO: クエリパラメタ認可
        params = await request.body()
        #assert token_info["date_from"] <= params["date_from"]
        #assert token_info["date_to"] <= params["date_to"]
        
        # API本体呼び出し
        response = await call_next(request)
        return response
    
    except Exception as e:
        # 認証・認可に失敗した場合
        response = Response(content="Unauthorized Request", status_code=401)
        return response