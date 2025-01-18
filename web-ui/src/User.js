import axios from 'axios';


export default async function getUser()
{
    try {
        let res = await axios.get("/api/me");
        return res.data;
    }
    catch (e)
    {
        console.log(e);
        return null;
    }
}