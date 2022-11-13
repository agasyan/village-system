import { Avatar, Card, CardContent, CardHeader, IconButton, Typography } from "@mui/material"
import { red } from '@mui/material/colors';

export const CommentCard = ({ comment, ...rest }) => {
    const formatDate = (time) => {
        var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
        return new Date(time*1000).toLocaleDateString("en-US", options)
      }
    return (
        <Card sx={{ width: "auto", mt: 1 }} {...rest} variant="outlined">
            <CardHeader
                avatar={
                    <Avatar style={{
                        backgroundColor: comment.color
                    }} aria-label="comment author">
                        {comment.created_user.full_name.charAt(0)}
                    </Avatar>
                }
                title={comment.created_user.full_name}
                subheader={formatDate(comment.updated_at_utc)}
            />
            <CardContent>
                <Typography variant="body2" color="text.secondary">
                    {comment.isi}
                </Typography>
            </CardContent>
        </Card >
    );
}