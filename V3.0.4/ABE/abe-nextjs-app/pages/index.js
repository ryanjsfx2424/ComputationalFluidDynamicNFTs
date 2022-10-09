import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import { useSession, signIn, signOut } from 'next-auth/react'
import { Flex, ChakraProvider } from '@chakra-ui/react'
import GuildCard from '../components/GuildCard'

let devMode = true;

// This was the redirect URI before...
//http://localhost:3000/api/auth/callback/discord

export default function Home() {
  if (!devMode) {
    var {data: session} = useSession()
  } else {
    var adminPerm = 2147483647
    var adminPermNew = '4398046511103'
    var manageServerPerm = 104189537
    var manageServerPermNew = '1071698529889'
    var session = {
      accessToken: process.env.NEXT_PUBLIC_discordAccessTokenDevMode,
      expires: "2022-11-05T08:58:07.626Z",
                user: 
                  {
                    image: "https://cdn.discordapp.com/embed/avatars/2.png",
                    name: "JeremyBearimy"
                  },
                userData: 
                  {
                    discriminator: "2207"
                  },
                guilds:
                {
                  0: 
                    {
                      icon: "719eedf706beb3fd201de80499edd278",
                      id: "789032594456576001",
                      name: "interactions.py",
                      owner: true,
                      permissions: 104713921,
                      permissions_new: "968619839169"
                    },
                  1:
                    {
                      icon: "084dd12134f3c21b9a82acbb814b1fe8",
                      id: "931482273440751638",
                      name: "ToTheMoonsNFT",
                      owner: false,
                      permissions: manageServerPerm,
                      permissions_new: manageServerPermNew
                    },
                  2:
                    {
                      icon: "9832210ac7bd13033037b865b1622c68",
                      id: "993961827799158925",
                      name: "Roo Tech",
                      owner: true,
                      permissions: 104189504,
                      permissions_new: "1071698529856"
                    }
                }
              }
  }

  console.log("session9: ", session)
  if (!session) {
    return (
      <div className={styles.container}>
        <Head>
          <title>ABE</title>
          <meta name="description" content="Always Be Early (ABE) by Ei Labs" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
  
        <main className={styles.main}>
          <h1 className={styles.title}>
            Always Be Early (ABE) by Ei Labs
          </h1>
          <div className="flex items-center justify-center h-screen bg-discord-gray text-white" >
            <button onClick={() => signIn('discord')}
                    className="bg-discord-blue text-xl px-5 py-3 rounded-md font-bold flex items-center space-x-4 hover:bg-gray-600 transition duration-75">
                <i className="fa-brands fa-discord text-2xl"></i>
                <span>Login with Discord</span>
            </button>
          </div>
        </main>
      </div>
    )
  } else {
    const {user, accessToken, guilds: guildsObj, userData} = session
    const guilds = Object.values(guildsObj).filter((guild) => ((guild.owner || guild.permissions & 0x8 || guild.permissions & 0x20)))
    console.log("35guilds: ", guilds)
    console.log("36 userData: ", userData)
  
    if (!accessToken) {
        console.log("No Access Token");
    }

    return (
      <div className={styles.container}>
        <Head>
          <title>ABE2</title>
          <meta name="description" content="Always Be Early (ABE) by Ei Labs" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
  
        <main className={styles.main}>
          <h1 className={styles.title}>
            Always Be Early (ABE) by Ei Labs2
          </h1>
          <h3>
            You are logged in!
          </h3>
          {user?.image && (
            <Image
              src={user.image}
              alt="Logged in user's discord pfp."
              width={38}
              height={38}
              style={{borderRadius: '50%'}}
              />
          )}
          Hello, {user?.name}#{userData.discriminator} <br />
          <button onClick={() => signOut()}>Sign Out</button>
          
          {guilds.map((guild) => (<GuildCard guild={guild} />))}
        </main>
      </div>
    )
} 
}
