import Head from 'next/head'
import Image from 'next/image'
import Bullet from '../components/bullet'

export default function Papers() {
    return (
        <>
            <Head>
                <title>RJF Papers</title>
                <meta name="description" content="Ryan Jefferey Farber's publications." />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <h2>Publications by Ryan Jeffrey Farber</h2>
            <p>
                <em>
                    <a href="https://scholar.google.com/citations?user=j1OaHHcAAAAJ&hl=en&oi=ao">Here</a> is my Google Scholar profile with citation information.
                </em>
            </p>
            <hr size="4"></hr>
            <h3>Articles in Refereed Journals</h3>
                <Bullet/>

            <h3>Books</h3>
                <Bullet/>
                &nbsp;
                Ryan Jeffrey Farber.
                <em>Parallel Universes Explained (Mysteries of Space)</em>
                Enslow Publishing, 2019.
        </>
    )
}