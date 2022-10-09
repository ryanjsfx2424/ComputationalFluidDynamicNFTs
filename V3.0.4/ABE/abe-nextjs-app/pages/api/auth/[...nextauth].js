import NextAuth from 'next-auth'
import DiscordProvider from 'next-auth/providers/discord'

// https://discord.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes
//const scopes = ['identify', 'guilds'].join(' ')
const scopes = 'identify guilds'

// NOTE: it is NOT possible to get guild channels from Oauth2 -- has to be done from a bot.

async function avoidRateLimit() {
  await sleep()
}

function sleep(ms = 1000) {
  return new Promise((res) => setTimeout(res, ms))
}

async function getUserData(token) {
  await avoidRateLimit()
  const fetch_result = await fetch("https://discord.com/api/users/@me", {
      headers: {
        authorization: `Bearer ${token}`,
      },
    })
  console.log("14 fetch_result: ", fetch_result)
  const data = await fetch_result.json()
  console.log("16 data: ", data)
  return data
}

async function getGuildData(token) {
  await avoidRateLimit()
  const fetch_result = await fetch('https://discord.com/api/users/@me/guilds', {
        headers: {
        authorization: `Bearer ${token}`,
      },
    })
  console.log("26 fetch_result: ", fetch_result)
  const data = await fetch_result.json()
  console.log("28 data: ", data)
  return data
}

export default NextAuth({
  providers: [
    DiscordProvider({
      clientId: process.env.DISCORD_CLIENT_ID,
      clientSecret: process.env.DISCORD_CLIENT_SECRET,
      authorization: {params: {scope: scopes}},
    }
    ),
  ],
  callbacks: {
    async jwt({ token, account }) {
      // Persist the OAuth access_token and or the user id to the token right after signin

      if (account) {
        token.accessToken = account.access_token
      }
      return token
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken


      // const userData = await getUserData(session.accessToken)
      // console.log("userData55: ", userData)
      //session.userData = userData

      // const guildData = await getGuildData(session.accessToken)

      // console.log("guildData59: ", guildData)
      // session.guilds = guildData

      return session
    }
  }
})
