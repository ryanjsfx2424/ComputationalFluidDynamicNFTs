import Image from 'next/image'
import Link from 'next/link'
import { Flex, ChakraProvider } from '@chakra-ui/react'
import Iframe from 'react-iframe'
import Modal from 'react-modal'
import { useState } from 'react'

export default function GuildCard(props) {
    let guild = props.guild;
    let state = { isOpen: false }
    const [isOpen, setIsOpen] = useState(false)

    const ABE_INVITE_LINK = "https://discord.com/oauth2/authorize?client_id=1014177171008409660&permissions=19456&scope=bot";

    return (
        <ChakraProvider>
            <Image 
                    src={'https://cdn.discordapp.com/icons/' + guild.id + "/" + guild.icon + '.jpg'}
                    alt={guild.name + ' PFP'}
                    width={38}
                    height={38}
                    style={{borderRadius: '50%'}}
            />

            <Flex direction="column">
                <h3>{guild.name}</h3>

                <Flex direction="row">
                    <a href={ABE_INVITE_LINK + "&guild_id=" + guild.id}>Add</a>
                    <Link href={'/settings/' + String(guild.name).toLowerCase() + '/' + guild.id}>Settings</Link>
                </Flex>
            </Flex>
        </ChakraProvider>
    )
}