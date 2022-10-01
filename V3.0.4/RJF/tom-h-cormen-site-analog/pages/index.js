import Head from 'next/head'
import Image from 'next/image'
import Link from 'next/link'
import styles from '../styles/Home.module.css'
import profilePic from '../public/profile.jpg'
import yellowSq from '../public/yellowsq.gif'
import Bullet from '../components/bullet'

export default function Home() {
  return (
    <>
      <div>
        <Head>
          <title>Ryan Jeffrey Farber</title>
          <meta name="description" content="Ryan Jefferey Farber's personal/research website." />
          <link rel="icon" href="/favicon.ico" />
        </Head>

        <table cellSpacing={0} cellPadding="10">
          <tbody>
            <tr valign="TOP">
              <td width="220" valign="TOP" align="LEFT">
                <Image 
                  src={profilePic} 
                  alt="Profile Picture"
                  ></Image>
                <p></p>
              </td>
              <td valign="TOP" align="LEFT">
                <h2 style={{paddingTop:"0", marginTop:"0"}}>
                  Ryan Jeffrey Farber
                  <br></br>
                  Postdoctoral Researcher
                  <br></br>
                  Max Planck Institute for Astrophysics (MPA)
                </h2>
                <p>
                  <strong>
                    I am nearing my one year anniversary at MPA! Say hi in room 020 :)
                  </strong>
                </p>
                <p>
                  <strong>
                    Update 29 September 2022: my fourth 1st author paper is on the arxiv!
                    <br></br>
                    <a href="https://arxiv.org/abs/2209.13622">Arxiv Link</a>
                  </strong>
                </p>
                <p>
                  Ph.D., <a href="https://umich.edu/">University of Michigan</a>, 2021.
                </p>
                <p></p>
                <dd>
                  <b>
                    <Bullet/>
                    &nbsp;
                    <Link href="/papers">Papers</Link>
                    <br></br>

                    <Bullet/>
                    &nbsp;
                    <Link href=".">Animations</Link>
                    <br></br>

                    <Bullet/>
                    &nbsp;
                    <Link href=".">C.V.</Link>
                  </b>
                </dd>
              </td>
            </tr>
          </tbody>
        </table>

        <hr></hr>
          I last taught in Winter 2020 as a graduate student instructor for ASTRO 102 Stars, Galaxies and the Universe.
          <p>
            I have six semesters (~three years) teaching experience, including as sole instructor for ASTRO 127.
          </p>
          
          <p>
            I designed the curriculum, assignments, and assessments for ASTRO 127: Naked Eye Astronomy in Spring 2018.
          </p>
        <hr></hr>
          From July through December 2019 I was a Graduate Fellow at the Kavli Institute for Theoretical Physics.
        <hr></hr>
        <h3>
          Contact Information
        </h3>
        Email:
        <br></br>
        <a href="mailto:ryanjsfx@mpa-garching.mpg.de">ryanjsfx@mpa-garching.mpg.de</a>
        <hr></hr>
      </div>
      <footer>
      Last modified: Thu 29 Sep 16:20:37 2022
      </footer>
    </>
  )
}
