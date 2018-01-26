import discord
import asyncio
import numpy as np

userlist = []
client = discord.Client()
#server = discord.Server()

Execution_environment = 'Mzg0MTI4NTc5NjMxNDQ4MDY0.DUtKmQ.vVzbX_gRw0NqKjIDDzC2BkfKA3o' #りすき鯖
#Execution_environment = 'NDA2MTUzOTY1MTY4ODg1NzYx.DUuz6Q.N5XVLA4tuBlGvpsZqLBLl6BnhIw' #xp鯖


@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('RSB Running...')
    
@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        
        num_all   = len(userlist)
        num_half  = num_all // 2

        id_all      = np.random.choice(num_all, num_all, replace=False)
        id_teamA    = list(id_all[0:num_half])
        id_teamB    = list(id_all[num_half:num_all])



        for n in id_teamA:
            print(userlist[n])

        for m in id_teamB:
            print(userlist[m])

    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    ## シャッフル機能
    elif message.content.startswith('!shuffle') and len(userlist) > 2:

        shuffle_result_msg = ''
        teamA_list  = []
        teamB_list  = []
        movefail_msg = ''

        num_all   = len(userlist)
        num_half  = num_all // 2

        id_all      = np.random.choice(num_all, num_all, replace=False)
        id_teamA    = list(id_all[0:num_half])
        id_teamB    = list(id_all[num_half:num_all])

        shuffle_result_msg += '```Markdown\n# Team A  \n'
        for n in id_teamA:
            shuffle_result_msg += userlist[n] + '\n'
            teamA_list.append(userlist[n])

        shuffle_result_msg += '\n# Team B  \n'
        for m in id_teamB:
            shuffle_result_msg += userlist[m] + '\n'
            teamB_list.append(userlist[m])
        
        shuffle_result_msg += '```'
        await client.send_message(message.channel, shuffle_result_msg)
        await asyncio.sleep(3)

        await client.send_message(message.channel,'ok? \n')
        msg = await client.wait_for_message(timeout=60,channel=message.channel)
        
        
        if msg.content == '!ok':
            try:
                teamA = await client.create_channel(message.server, 'Team - A', type=discord.ChannelType.voice)
                teamB = await client.create_channel(message.server, 'Team - B', type=discord.ChannelType.voice)
            except:
                await client.send_message(message.channel,'```Markdown\nError : channel create failed.```')
                print('Exception :  channel create failed ')
            #await asyncio.sleep(3)
            for member in client.get_all_members():
                if member.name in teamA_list:
                    try:
                        result = await client.move_member(member,teamA)
                        teamA_list.remove(member.name)
                    except:
                        await client.send_message(message.channel,' Error :' + member.name +' move failed.')
                        print(' Error :' + member.name +' move failed.')
                        teamA_list.remove(member.name)
                elif member.name in teamB_list:
                    try:
                        result = await client.move_member(member,teamB)
                        teamB_list.remove(member.name)
                    except:
                        await client.send_message(message.channel,' Error :' + member.name +' move failed.')
                        print(' Error :' + member.name +' move failed.')
                #await asyncio.sleep(3)
                        teamB_list.remove(member.name)
            if len(teamA_list) > 0:
                for tA in teamA_list:
                    movefail_msg += tA + '\n'
            if len(teamB_list) > 0:
                for tB in teamB_list:
                    movefail_msg += tB + '\n'
            if len(movefail_msg) > 0:
                movefail_msg = '```Markdown\nError : move failed\n' + movefail_msg + '```'
                await client.send_message(message.channel,movefail_msg)

            await asyncio.sleep(3)
            await client.send_message(message.channel,'Move complete.')

    ## メンバー追加処理
    elif message.content.startswith('!join') and len(message.content) > 6:
        try:
            join_msg = ''
            name = message.content[6:len(message.content)]
            if name.find(',') > 0:
                #join_msg += ' #User joined : \n'
                for x in name.split(','):
                    if x not in userlist:
                        userlist.append(x)
                        join_msg += x + '\n'
                    else:
                        join_msg += x + ' has already been joined.\n'
                        
                join_msg = '```Markdown\n#User joined : \n' + join_msg + '```'
                await client.send_message(message.channel,join_msg)
            else:
                if name not in userlist:
                    userlist.append(name)
                    await client.send_message(message.channel, '#User joined : ' + name)
                else:
                    await client.send_message(message.channel, name + ' has already been joined.')
        except:
            await client.send_message(message.channel,' Error : join failed.')
            print('Exception : !join ')
    ## 退出処理
    elif message.content.startswith('!leave') and len(message.content) > 7:
        ### ToDo : カンマ区切りで退出機能
        try:
            name = message.content[7:len(message.content)]
            userlist.remove(name)
            
            await client.send_message(message.channel,name + ' has leave.')
        except ValueError:
            await client.send_message(message.channel,' Error : User not found.\n　　　Failed to leave.')
        except:
            print('Exception : !leave ')
    ## リストクリア処理
    elif message.content.startswith('!clear'):
        try:
            userlist.clear()
            await client.send_message(message.channel, ' Clear complete.')
        except:
            await client.send_message(message.channel,' Error : clear failed.')
            print('Exception : !clear ')
    ## リスト羅列
    elif message.content.startswith('!show'):
        ### ToDo : for分で文字列結合後,一括で発言
        try:
            if len(userlist) > 0:
                for n in userlist:
                    await client.send_message(message.channel, n)
            else:
                await client.send_message(message.channel,' Error : Not found join users.')
        except:
            print('Exception : !show ')
    elif message.content.startswith('!help'):
        help_msg = ''
        help_msg += '```Markdown\n#Command\n'
        help_msg += '!join      : Discord上の名前(#以降は入れずに)を入力することで登録することができる. カンマ区切りで一括登録可能.\n'
        help_msg += '!leave     : Discord上の名前(#以降は入れずに)を入力することで登録解除することができる.\n'
        help_msg += '!shuffle   : 登録ユーザーをランダムにチーム分けした後,結果を表示. 確認メッセージ後,数秒間ほどあけて!okと入力することによりボイスチャンネルの移動が行われる.\n'
        help_msg += '再度シャッフルしたい場合,任意の文字列を発言後!shuffleで可能\n'
        help_msg += '!clear     : 全登録を消去することができる.\n'
        help_msg += '!show      : 現在登録されているユーザーを確認することができる.\n'
        help_msg += '```'
        await client.send_message(message.channel,help_msg)
client.run(Execution_environment)