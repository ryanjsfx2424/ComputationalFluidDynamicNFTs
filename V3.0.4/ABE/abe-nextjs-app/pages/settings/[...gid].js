import { useState, useEffect, useCallback } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { useRouter } from 'next/router'
import abePfp from '../../public/images/abe_pfp.webp'
import {
    ChakraProvider,
    Flex,
    Menu,
    MenuButton,
    MenuList,
    MenuItem,
    MenuItemOption,
    MenuGroup,
    MenuOptionGroup,
    MenuDivider,
  } from '@chakra-ui/react'

export default function Settings() {
    const router = useRouter()
    const { guildName, guildId } = router.query
    const gid = guildId
    console.log("router.query: ", router.query)
    console.log("FUDGE");
    // console.log("guildName: ", guildName)
    // console.log("guildId: ", guildId)
    // console.log("gid: ", gid)

    const [finishedFetch, setFinishedFetch] = useState(false)
    const [guildData, setGuildData] = useState([])
    const [currentGuild, setCurrentGuild] = useState("")
    const [addingChannel, setAddingChannel] = useState(false)
    const [guildChannels, setGuildChannels] = useState(["general", "bot-commands", "the-lodge", "cfd-v1"])

    let token = process.env.NEXT_PUBLIC_discordAccessTokenDevMode
    // console.log("process.env.NEXT_PUBLIC_discordAccessTokenDevMode: ", process.env.NEXT_PUBLIC_discordAccessTokenDevMode)
    // console.log("token: ", token)

    async function avoidRateLimit() {
        await sleep()
    }
      
    function sleep(ms = 2000) {
        return new Promise((res) => setTimeout(res, ms))
    }

    const fetchGuildData = useCallback(async() => {
        await avoidRateLimit()
        let response = await fetch('https://discord.com/api/users/@me/guilds', {
            headers: {
                authorization: `Bearer ${token}`,
        }})
        response = await response.json()

        // set current guild
        for (const [key,value] of Object.entries(response)) {
            if (Number(value.id) === Number(gid) ) {
                setCurrentGuild(value.name)
            }
        }

        response = Object.values(response).filter((guild) => (true))//(guild.owner || guild.permissions & 0x8 || guild.permissions & 0x20)))
        // console.log("45 response: ", response);

        setGuildData(response)
        setFinishedFetch(true)
    })


    useEffect(() => {
        fetchGuildData()
    }, [])

    return (
        <ChakraProvider>
            <Flex direction="column">
                <h1>Guild Id: {gid}</h1>

                <Link href="/">
                    <a>
                        <Image
                            src={abePfp}
                            alt="abe pfp"
                            width={38}
                            height={38}
                        />
                    </a>
                </Link>

                {(!finishedFetch || guildData.length === 0) ?
                    <Menu>
                        <MenuButton>
                            {guildName}
                        </MenuButton>
                        <MenuList>
                            <MenuItem>Other Guild Name</MenuItem>
                            <MenuItem>Some Dif Guild Name</MenuItem>
                            <MenuItem>Not Another Guild!</MenuItem>
                        </MenuList>
                    </Menu>
                :
                    <Menu>
                        <MenuButton>
                            {currentGuild}
                        </MenuButton>
                        <MenuList>
                            {/* {console.log("88 guildData [gid].js: ", guildData, {})}
                            {console.log(guildData === {})}
                            {console.log("90 typeOf guildData [gid].js: ",typeof(guildData))}
                            {console.log("91 typeOf {} [gid].js: ",typeof({}))} */}
                            {guildData.map((guild) => (<MenuItem>{guild.name}</MenuItem>))}
                        </MenuList>
                    </Menu>


                }
                <Menu>
                    <MenuButton>
                        Add Feed
                    </MenuButton>
                    <MenuList>
                        {guildChannels.map((channel) => (<MenuItem>{channel.name}</MenuItem>))}
                    </MenuList>
                </Menu>
            </Flex>
        </ChakraProvider>
    )
}