from bucketlist.models import BucketList, BucketlistItem
from apiv1.serializer import BucketListSerializer, BucketItemSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BucketListView(APIView):

    """
    List all buckets, or create a new bucket.
    """

    # gets all buckets from the database

    def get(self, request):
        buckets = BucketList.objects.filter(author_id=self.request.user)
        serializer = BucketListSerializer(buckets, many=True)
        return Response(serializer.data)

    # creates a new bucket
    def post(self, request):
        serializer = BucketListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BucketListEditView(APIView):

    """
    Retrieve, Update of delete a bucketlist
    """

    # checks the bucket exists in the database

    def get_object(self, bucketlistid):
        bucket = BucketList.objects.filter(
            pk=bucketlistid,
            author_id=self.request.user).first()
        if bucket:
            return bucket
        else:
            raise Http404

    # gets the bucket
    def get(self, request, bucketlistid):
        bucket = self.get_object(bucketlistid)
        serializer = BucketListSerializer(bucket)
        return Response(serializer.data)

    # edit bucket
    def put(self, request, bucketlistid):
        bucket = self.get_object(bucketlistid)
        # request.data['author'] = bucket.author_id
        serializer = BucketListSerializer(bucket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete bucket
    def delete(self, request, bucketlistid):
        bucket = self.get_object(bucketlistid)
        bucket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BucketItemView(APIView):

    """
    Create a bucketitem
    """

    # checks the bucketlist for the bucketitem exists

    def get_object(self, bucketlistid):
        bucket = BucketList.objects.filter(
            pk=bucketlistid,
            author_id=self.request.user).first()
        if bucket:
            return bucket
        else:
            raise Http404

    # adds a new bucketitem
    def post(self, request, bucketlistid):
        bucket = self.get_object(bucketlistid)
        # request.data['bucketlist'] = bucket.id
        serializer = BucketItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(bucketlist=bucket.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BucketItemEditView(APIView):

    """
    Retrieve, Update of delete a bucketitem
    """

    # checks the bucketitem exists

    def get_object(self, bucketlistid, bucketitemid):
        bucket = BucketList.objects.filter(
            pk=bucketlistid,
            author_id=self.request.user).first()
        bucketitem = BucketlistItem.objects.filter(
            pk=bucketitemid, bucketlist_id=bucket).first()
        if bucket and bucketitem:
            return bucketitem
        else:
            raise Http404

    # get a bucketitem
    def get(self, request, bucketlistid, bucketitemid):
        bucketitem = self.get_object(bucketlistid, bucketitemid)
        serializer = BucketItemSerializer(bucketitem)
        return Response(serializer.data)

    # edit a bucketitem
    def put(self, request, bucketlistid, bucketitemid):
        bucketitem = self.get_object(bucketlistid, bucketitemid)
        request.data['bucketlist'] = bucketitem.bucketlist_id
        if 'name' not in request.data.keys():
            request.data['name'] = bucketitem.name
        serializer = BucketItemSerializer(bucketitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a bucketitem
    def delete(self, request, bucketlistid, bucketitemid):
        bucketitem = self.get_object(bucketlistid, bucketitemid)
        bucketitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)