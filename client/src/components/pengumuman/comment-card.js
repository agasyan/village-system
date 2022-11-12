import { Avatar, Card, CardContent, CardHeader, IconButton, Typography } from "@mui/material"
import { red } from '@mui/material/colors';

export const CommentCard = ({ comment, ...rest }) => {
    const randomColor = () => {
        let hex = Math.floor(Math.random() * 0xFFFFFF);
        let color = "#" + hex.toString(16);

        return color;
    }
    const formatDate = (time) => {
        var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
        return new Date(time*1000).toLocaleDateString("en-US", options)
      }
    return (
        <Card sx={{ width: "auto", mt: 1 }} {...rest} variant="outlined">
            <CardHeader
                avatar={
                    <Avatar style={{
                        backgroundColor: randomColor()
                    }} aria-label="comment author">
                        {comment.author.charAt(0)}
                    </Avatar>
                }
                title={comment.author}
                subheader={formatDate(comment.created_at)}
            />
            <CardContent>
                <Typography variant="body2" color="text.secondary">
                    {comment.content}
                </Typography>
            </CardContent>
        </Card >
    );
}